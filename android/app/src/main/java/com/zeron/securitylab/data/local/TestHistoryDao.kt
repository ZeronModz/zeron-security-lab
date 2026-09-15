package com.zeron.securitylab.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface TestHistoryDao {
    @Query("SELECT * FROM test_history ORDER BY createdAt DESC")
    fun getAll(): Flow<List<TestHistoryEntity>>

    @Query("SELECT * FROM test_history WHERE id = :id")
    suspend fun getById(id: String): TestHistoryEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(entity: TestHistoryEntity)

    @Query("DELETE FROM test_history WHERE id = :id")
    suspend fun deleteById(id: String)

    @Query("DELETE FROM test_history")
    suspend fun deleteAll()

    @Query("SELECT COUNT(*) FROM test_history")
    fun getCount(): Flow<Int>
}
