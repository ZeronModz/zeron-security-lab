package com.zeron.securitylab.ui.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Api
import androidx.compose.material.icons.filled.BrowseGallery
import androidx.compose.material.icons.filled.Dashboard
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.filled.Settings
import androidx.compose.ui.graphics.vector.ImageVector

sealed class Screen(val route: String, val title: String, val icon: ImageVector) {
    data object Dashboard : Screen("dashboard", "Dashboard", Icons.Default.Dashboard)
    data object WebTesting : Screen("web_testing", "Web Testing", Icons.Default.Language)
    data object ApiTesting : Screen("api_testing", "API Testing", Icons.Default.Api)
    data object BrowserLab : Screen("browser_lab", "Browser Lab", Icons.Default.BrowseGallery)
    data object History : Screen("history", "History", Icons.Default.History)
    data object Settings : Screen("settings", "Settings", Icons.Default.Settings)
}

val bottomNavItems = listOf(
    Screen.Dashboard,
    Screen.WebTesting,
    Screen.ApiTesting,
    Screen.BrowserLab,
    Screen.History,
    Screen.Settings,
)
