package com.zeron.securitylab.data.api

import kotlinx.serialization.Serializable

@Serializable
data class ApiResponse<T>(
    val success: Boolean,
    val data: T? = null,
    val error: ErrorData? = null,
    val request_id: String? = null
)

@Serializable
data class ErrorData(
    val code: String,
    val message: String
)

@Serializable
data class HealthData(
    val status: String,
    val version: String,
    val database: String,
    val browser: String,
    val cloudflare: String,
    val recaptcha: String
)

@Serializable
data class SystemInfoData(
    val app_name: String,
    val version: String,
    val python_version: String,
    val platform: String,
    val uptime_seconds: Int,
    val database_type: String
)

@Serializable
data class WebFetchRequest(
    val url: String,
    val method: String = "GET",
    val headers: Map<String, String> = emptyMap(),
    val cookies: Map<String, String> = emptyMap(),
    val body: String? = null,
    val timeout: Int = 30,
    val follow_redirects: Boolean = true,
    val verify_ssl: Boolean = true
)

@Serializable
data class WebFetchResponseData(
    val url: String,
    val status_code: Int,
    val response_time_ms: Int,
    val headers: Map<String, String>,
    val body: String,
    val redirect_chain: List<String> = emptyList(),
    val cookies: Map<String, String> = emptyMap(),
    val security_headers: Map<String, String?> = emptyMap()
)

@Serializable
data class ApiRequestModel(
    val url: String,
    val method: String = "GET",
    val headers: Map<String, String> = emptyMap(),
    val query_params: Map<String, String> = emptyMap(),
    val body: String? = null,
    val body_type: String = "raw",
    val auth_type: String? = null,
    val auth_value: String? = null,
    val timeout: Int = 30
)

@Serializable
data class TargetData(
    val id: String,
    val url: String,
    val name: String? = null,
    val description: String? = null,
    val is_authorized: Boolean = false,
    val created_at: String
)

@Serializable
data class CloudflareHealthData(
    val available: Boolean,
    val server_url: String,
    val version: String,
    val engine: String,
    val status: String,
    val error: String? = null,
    val note: String? = null
)

@Serializable
data class RecaptchaHealthData(
    val available: Boolean,
    val server_url: String,
    val version: String,
    val engine: String,
    val status: String,
    val error: String? = null,
    val note: String? = null,
    val test_keys_available: Boolean = false,
    val manual_mode: Boolean = false
)

@Serializable
data class HistoryEntry(
    val entries: List<HistoryItem>,
    val total: Int,
    val page: Int,
    val per_page: Int
)

@Serializable
data class HistoryItem(
    val id: String,
    val test_type: String,
    val target_url: String? = null,
    val status: String,
    val status_code: Int? = null,
    val response_time_ms: Int? = null,
    val created_at: String
)
