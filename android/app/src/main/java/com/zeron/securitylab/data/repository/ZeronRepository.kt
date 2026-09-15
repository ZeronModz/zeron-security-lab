package com.zeron.securitylab.data.repository

import com.zeron.securitylab.data.api.ApiClient
import com.zeron.securitylab.data.api.ApiResponse
import com.zeron.securitylab.data.api.HealthData
import com.zeron.securitylab.data.api.WebFetchRequest
import com.zeron.securitylab.data.api.WebFetchResponseData
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class ZeronRepository {
    private val api = ApiClient.api

    suspend fun health(): Result<HealthData> = withContext(Dispatchers.IO) {
        try {
            val response = api.health()
            if (response.success && response.data != null) {
                Result.success(response.data)
            } else {
                Result.failure(Exception(response.error?.message ?: "Unknown error"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun webFetch(request: WebFetchRequest): Result<WebFetchResponseData> = withContext(Dispatchers.IO) {
        try {
            val response = api.webFetch(request)
            if (response.success && response.data != null) {
                Result.success(response.data)
            } else {
                Result.failure(Exception(response.error?.message ?: "Unknown error"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun apiRequest(request: com.zeron.securitylab.data.api.ApiRequestModel): Result<Map<String, Any>> = withContext(Dispatchers.IO) {
        try {
            val response = api.apiRequest(request)
            if (response.success && response.data != null) {
                Result.success(response.data)
            } else {
                Result.failure(Exception(response.error?.message ?: "Unknown error"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun listTargets(): Result<List<Map<String, Any>>> = withContext(Dispatchers.IO) {
        try {
            val response = api.listTargets()
            if (response.success && response.data != null) {
                @Suppress("UNCHECKED_CAST")
                val targets = response.data["targets"] as? List<Map<String, Any>> ?: emptyList()
                Result.success(targets)
            } else {
                Result.failure(Exception(response.error?.message ?: "Unknown error"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun cloudflareHealth(): Result<Map<String, Any>> = withContext(Dispatchers.IO) {
        try {
            val response = api.cloudflareHealth()
            if (response.success && response.data != null) {
                @Suppress("UNCHECKED_CAST")
                Result.success(response.data as Map<String, Any>)
            } else {
                Result.failure(Exception(response.error?.message ?: "Unknown error"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun recaptchaHealth(): Result<Map<String, Any>> = withContext(Dispatchers.IO) {
        try {
            val response = api.recaptchaHealth()
            if (response.success && response.data != null) {
                @Suppress("UNCHECKED_CAST")
                Result.success(response.data as Map<String, Any>)
            } else {
                Result.failure(Exception(response.error?.message ?: "Unknown error"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
