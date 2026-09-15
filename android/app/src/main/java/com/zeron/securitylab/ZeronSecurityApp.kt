package com.zeron.securitylab

import android.app.Application
import com.zeron.securitylab.data.local.AppDatabase

class ZeronSecurityApp : Application() {
    val database: AppDatabase by lazy { AppDatabase.getInstance(this) }
}
