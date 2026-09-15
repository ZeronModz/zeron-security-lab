package com.zeron.securitylab.data.api

import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path
import java.util.concurrent.TimeUnit

interface ZeronApi {

    @GET("/api/v1/health")
    suspend fun health(): ApiResponse<HealthData>

    @GET("/api/v1/system/info")
    suspend fun systemInfo(): ApiResponse<SystemInfoData>

    @GET("/api/v1/system/capabilities")
    suspend fun systemCapabilities(): ApiResponse<Map<String, Any>>

    @POST("/api/v1/web/fetch")
    suspend fun webFetch(@Body request: WebFetchRequest): ApiResponse<WebFetchResponseData>

    @POST("/api/v1/web/render")
    suspend fun webRender(@Body request: WebFetchRequest): ApiResponse<Map<String, Any>>

    @POST("/api/v1/api/request")
    suspend fun apiRequest(@Body request: ApiRequestModel): ApiResponse<Map<String, Any>>

    @GET("/api/v1/targets")
    suspend fun listTargets(): ApiResponse<Map<String, Any>>

    @POST("/api/v1/targets")
    suspend fun createTarget(@Body request: Map<String, Any>): ApiResponse<TargetData>

    @DELETE("/api/v1/targets/{id}")
    suspend fun deleteTarget(@Path("id") id: String): ApiResponse<Map<String, Any>>

    @GET("/api/v1/cloudflare/health")
    suspend fun cloudflareHealth(): ApiResponse<CloudflareHealthData>

    @POST("/api/v1/cloudflare/test")
    suspend fun cloudflareTest(@Body request: Map<String, Any>): ApiResponse<Map<String, Any>>

    @GET("/api/v1/recaptcha/health")
    suspend fun recaptchaHealth(): ApiResponse<RecaptchaHealthData>

    @POST("/api/v1/recaptcha/test")
    suspend fun recaptchaTest(@Body request: Map<String, Any>): ApiResponse<Map<String, Any>>

    @GET("/api/v1/history")
    suspend fun history(): ApiResponse<HistoryEntry>
}

object ApiClient {
    private const val PRODUCTION_URL = "https://backend-production-cd11.up.railway.app"
    private const val EMULATOR_URL = "http://10.0.2.2:8000"

    private val json = Json {
        ignoreUnknownKeys = true
        isLenient = true
        coerceInputValues = true
    }

    private val loggingInterceptor = HttpLoggingInterceptor().apply {
        level = HttpLoggingInterceptor.Level.BODY
    }

    private val httpClient = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .addInterceptor(loggingInterceptor)
        .build()

    private val retrofit = Retrofit.Builder()
        .baseUrl(PRODUCTION_URL)
        .client(httpClient)
        .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
        .build()

    val api: ZeronApi = retrofit.create(ZeronApi::class.java)

    fun createApi(baseUrl: String): ZeronApi {
        val customRetrofit = Retrofit.Builder()
            .baseUrl(baseUrl)
            .client(httpClient)
            .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
            .build()
        return customRetrofit.create(ZeronApi::class.java)
    }
}
