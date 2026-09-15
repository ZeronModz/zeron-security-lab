package com.zeron.securitylab.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "test_history")
data class TestHistoryEntity(
    @PrimaryKey val id: String,
    val testType: String,
    val targetUrl: String,
    val statusCode: Int?,
    val responseTimeMs: Int?,
    val status: String,
    val createdAt: Long,
    val rawResponse: String? = null
)
