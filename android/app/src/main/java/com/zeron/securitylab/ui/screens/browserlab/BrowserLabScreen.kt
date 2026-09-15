package com.zeron.securitylab.ui.screens.browserlab

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Send
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.zeron.securitylab.ui.theme.Error
import com.zeron.securitylab.ui.theme.OnBackground
import com.zeron.securitylab.ui.theme.OnSurface
import com.zeron.securitylab.ui.theme.OnSurfaceVariant
import com.zeron.securitylab.ui.theme.Primary
import com.zeron.securitylab.ui.theme.Surface
import com.zeron.securitylab.ui.theme.SurfaceVariant
import com.zeron.securitylab.ui.theme.Warning

@Composable
fun BrowserLabScreen() {
    var url by remember { mutableStateOf("") }
    var selectedTab by remember { mutableIntStateOf(0) }

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        item {
            Text(
                text = "Browser Lab",
                style = MaterialTheme.typography.headlineMedium,
                color = OnBackground,
                fontWeight = FontWeight.Bold,
            )
            Text(
                text = "Authorized browser testing with JavaScript rendering",
                style = MaterialTheme.typography.bodyMedium,
                color = OnSurfaceVariant,
            )
        }

        item {
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = Surface),
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    OutlinedTextField(
                        value = url,
                        onValueChange = { url = it },
                        label = { Text("Target URL") },
                        placeholder = { Text("https://your-authorized-site.com") },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true,
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Primary,
                            focusedLabelColor = Primary,
                        ),
                    )

                    Spacer(modifier = Modifier.height(12.dp))

                    TabRow(
                        selectedTabIndex = selectedTab,
                        containerColor = Surface,
                        contentColor = Primary,
                    ) {
                        Tab(selected = selectedTab == 0, onClick = { selectedTab = 0 }) {
                            Text("Standard", modifier = Modifier.padding(12.dp))
                        }
                        Tab(selected = selectedTab == 1, onClick = { selectedTab = 1 }) {
                            Text("Cloudflare Test", modifier = Modifier.padding(12.dp))
                        }
                        Tab(selected = selectedTab == 2, onClick = { selectedTab = 2 }) {
                            Text("CAPTCHA Test", modifier = Modifier.padding(12.dp))
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    when (selectedTab) {
                        0 -> Text(
                            "Standard browser testing with JavaScript execution and network monitoring.",
                            color = OnSurfaceVariant,
                        )
                        1 -> {
                            Text(
                                "Authorized Cloudflare protection testing on your own domains.",
                                color = OnSurfaceVariant,
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Card(
                                colors = CardDefaults.cardColors(containerColor = Warning.copy(alpha = 0.1f)),
                                shape = RoundedCornerShape(8.dp),
                            ) {
                                Row(modifier = Modifier.padding(12.dp)) {
                                    Icon(Icons.Default.Warning, contentDescription = null, tint = Warning)
                                    Spacer(modifier = Modifier.padding(4.dp))
                                    Text(
                                        "Only use on domains you own or have explicit authorization to test.",
                                        color = Warning,
                                        style = MaterialTheme.typography.bodySmall,
                                    )
                                }
                            }
                        }
                        2 -> {
                            Text(
                                "reCAPTCHA integration testing with official test keys.",
                                color = OnSurfaceVariant,
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Card(
                                colors = CardDefaults.cardColors(containerColor = Warning.copy(alpha = 0.1f)),
                                shape = RoundedCornerShape(8.dp),
                            ) {
                                Row(modifier = Modifier.padding(12.dp)) {
                                    Icon(Icons.Default.Warning, contentDescription = null, tint = Warning)
                                    Spacer(modifier = Modifier.padding(4.dp))
                                    Text(
                                        "Supports official test keys and manual verification flow.",
                                        color = Warning,
                                        style = MaterialTheme.typography.bodySmall,
                                    )
                                }
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(16.dp))

                    Button(
                        onClick = { },
                        modifier = Modifier.fillMaxWidth(),
                        enabled = url.isNotBlank(),
                        colors = ButtonDefaults.buttonColors(containerColor = Primary),
                        shape = RoundedCornerShape(12.dp),
                    ) {
                        Icon(Icons.Default.Send, contentDescription = null)
                        Spacer(modifier = Modifier.padding(4.dp))
                        Text("Launch Browser Test")
                    }
                }
            }
        }

        item {
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = SurfaceVariant),
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        "Browser Engine Status",
                        color = OnBackground,
                        fontWeight = FontWeight.SemiBold,
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        "Browser-based testing requires a Linux server environment. " +
                        "Deploy the backend on Railway or a VPS for full browser support.",
                        color = OnSurfaceVariant,
                        style = MaterialTheme.typography.bodySmall,
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                    ) {
                        Text("CloakBrowser", color = OnSurfaceVariant)
                        Text("Requires Linux", color = Warning)
                    }
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                    ) {
                        Text("DrissionPage", color = OnSurfaceVariant)
                        Text("Requires Linux", color = Warning)
                    }
                }
            }
        }
    }
}
