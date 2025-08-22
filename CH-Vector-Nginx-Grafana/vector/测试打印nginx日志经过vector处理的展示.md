```yaml
# 1. 定义输入源（读取日志文件）
sources:
  nginx_access_log:  # 自定义 source 名称
    type: "file"
    include:
      - "/nginx_logs/access.log"  # YAML 数组用短横线表示
    read_from: "beginning"  # 可选参数：从文件开头读取

# 2. 定义日志解析逻辑（VRL 脚本）
transforms:
  parse_json:  # 自定义 transform 名称
    type: "remap"
    inputs:  # 指定输入源的名称（对应 sources 中的名称）
      - "nginx_access_log"
    source: |  # 用 | 保留多行文本格式（VRL 代码块）
      # 解析 JSON 日志消息
      #. = parse_json!(.message)
      #
      .message = string!(.message)
      if contains(.message,"\\x") { .message = replace(.message, "\\x", "\\\\x") }
      . = parse_json!(.message)
      .createdtime = to_unix_timestamp(now(), unit: "milliseconds")
      .timestamp = to_unix_timestamp(parse_timestamp!(.timestamp , format: "%+"), unit: "milliseconds")
      .url_list = split!(.url, "?", 2)
      .path = .url_list[0]
      .query = .url_list[1]
      .path_list = split!(.path, "/", 3)
      if length(.path_list) > 2 {.top_path = join!(["/", .path_list[1]])} else {.top_path = "/"}
      .duration = round(((to_float(.responsetime) ?? 0) - (to_float(.upstreamtime) ?? 0)) ?? 0,3)
      if .xff == "-" { .xff = .remote_ip }
      .client_ip = split!(.xff, ",", 2)[0]
      .ua = parse_user_agent!(.http_user_agent , mode: "enriched")
      .client_browser_family = .ua.browser.family
      .client_browser_major = .ua.browser.major
      .client_os_family = .ua.os.family
      .client_os_major = .ua.os.major
      .client_device_brand = .ua.device.brand
      .client_device_model = .ua.device.model
      .geoip = get_enrichment_table_record("geoip_table", {"ip": .client_ip}) ?? {"city_name":"unknown","region_name":"unknown","country_name":"unknown"}
      .client_city = .geoip.city_name
      .client_region = .geoip.region_name
      .client_country = .geoip.country_name
      .client_latitude = .geoip.latitude
      .client_longitude = .geoip.longitude
      del(.path_list)
      del(.url_list)
      del(.ua)
      del(.geoip)
      del(.url)
      # 类型转换（可选）
      .status = to_int!(.status)
      .response_length = to_int!(.response_length)
      .responsetime = to_float!(.responsetime)

# 3. 定义输出目标（控制台打印）
sinks:
  console_output:  # 自定义 sink 名称
    type: "console"
    inputs:
      - "parse_json"  # 指向 transform 名称
    encoding:
      codec: "json"  # 输出格式为 JSO

  ```
