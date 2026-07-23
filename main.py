import datetime

# --- Simulated Data Sources (Context Providers) ---
# In a real AIOps system, these would be integrations with monitoring tools, CMDBs, CI/CD pipelines, etc.

def get_current_system_metrics(server_id):
    """Simulates fetching current system metrics for a given server."""
    # This data is crucial for understanding the overall health and correlating issues.
    if server_id == "server-001":
        return {
            "cpu_usage_percent": 95,  # The primary anomaly detected
            "memory_usage_percent": 70, # Context: Is memory also high?
            "disk_io_rate_mbps": 120,   # Context: Is disk I/O a factor?
            "network_latency_ms": 5,    # Context: Is network healthy?
            "service_status": {"web_app": "running", "db_service": "running"}
        }
    return {}

def get_recent_deployment_history(server_id):
    """Simulates fetching recent deployment history for a server."""
    # Recent changes are a common cause of incidents; this provides crucial context.
    if server_id == "server-001":
        return [
            {"timestamp": datetime.datetime.now() - datetime.timedelta(hours=1), "change": "App v2.1 deployed", "status": "success"},
            {"timestamp": datetime.datetime.now() - datetime.timedelta(days=3), "change": "OS patch applied", "status": "success"},
        ]
    return []

def get_business_service_dependencies(server_id):
    """Simulates identifying business services dependent on this server."""
    # Understanding the business impact helps prioritize and communicate effectively.
    if server_id == "server-001":
        return ["Customer Portal", "API Gateway", "Internal Reporting"]
    return []

def get_scheduled_tasks(server_id, current_time):
    """Simulates checking for scheduled tasks that might explain resource spikes."""
    # Known activities can be filtered out as non-incidents, providing context for expected behavior.
    if server_id == "server-001" and current_time.hour == datetime.datetime.now().hour:
         return ["Hourly Data Sync", "Log Rotation"]
    return []

# --- AI-Powered Incident Assessment ---

def assess_incident_with_context(server_id, anomaly_details):
    """
    This function simulates an AI's decision-making process.
    It gathers various contextual data points to provide a more informed assessment
    than a simple threshold alert, demonstrating 'effective context creation'.
    """
    print(f"\n--- AI Contextual Assessment for {server_id} ---")
    current_time = datetime.datetime.now()

    # 1. Gather Context: System-wide metrics (beyond the initial anomaly)
    all_metrics = get_current_system_metrics(server_id)
    print(f"  - Full System Metrics: {all_metrics}")

    # 2. Gather Context: Recent changes/deployments
    deployments = get_recent_deployment_history(server_id)
    print(f"  - Recent Deployments: {deployments}")

    # 3. Gather Context: Business impact
    impacted_services = get_business_service_dependencies(server_id)
    print(f"  - Dependent Business Services: {impacted_services}")

    # 4. Gather Context: Scheduled maintenance/tasks
    scheduled_tasks = get_scheduled_tasks(server_id, current_time)
    print(f"  - Active/Upcoming Scheduled Tasks: {scheduled_tasks}")

    # --- AI-like Decision Logic based on Context ---
    # This is where the AI uses the gathered context to make a nuanced decision.
    assessment = "Unknown"
    severity = "Informational"
    recommendation = "Monitor system"

    if anomaly_details["metric"] == "cpu_usage_percent":
        cpu_value = anomaly_details["value"]
        print(f"  Anomaly: CPU usage is {cpu_value}%")

        # Contextual Rule 1: Is it a known scheduled task?
        if "Hourly Data Sync" in scheduled_tasks:
            assessment = "Expected Load"
            severity = "Low"
            recommendation = "High CPU is due to scheduled hourly data synchronization. No immediate action required, but monitor for duration."
            print("  -> Context: High CPU aligns with a scheduled task. This is not a true incident.")
        # Contextual Rule 2: Is it correlated with other severe issues?
        elif all_metrics.get("memory_usage_percent", 0) > 85:
            assessment = "Critical Incident"
            severity = "High"
            recommendation = "High CPU and Memory usage detected. This indicates a severe resource bottleneck. Investigate process utilization immediately."
            print("  -> Context: High CPU is correlated with high memory usage, indicating a more severe issue.")
        # Contextual Rule 3: Is it after a recent deployment?
        elif any(d["timestamp"] > current_time - datetime.timedelta(hours=2) and d["status"] == "success" for d in deployments):
            assessment = "Potential Regression"
            severity = "Medium"
            recommendation = "High CPU detected shortly after a recent successful deployment. Investigate if the new deployment introduced performance issues. Consider rollback if impact is significant."
            print("  -> Context: High CPU occurred after a recent deployment, suggesting a potential regression.")
        # Default assessment if no specific context matches
        else:
            assessment = "Unexplained Anomaly"
            severity = "Medium"
            recommendation = f"High CPU usage detected affecting services like {', '.join(impacted_services)}. No clear contextual explanation found. Investigate root cause."
            print("  -> Context: No specific contextual match found, treating as an unexplained anomaly.")
    
    return {
        "assessment": assessment,
        "severity": severity,
        "recommendation": recommendation
    }

# --- Main Monitoring Loop (Simplified) ---

def monitor_system(server_id):
    """
    Simulates a monitoring agent detecting an anomaly and
    triggering an AI-powered contextual assessment.
    """
    print(f"--- Monitoring System: {server_id} ---")
    
    # Get current metrics for initial anomaly detection
    current_metrics = get_current_system_metrics(server_id)
    
    # Traditional Anomaly Detection (simple threshold)
    if current_metrics.get("cpu_usage_percent", 0) > 90:
        print(f"  Traditional Alert: CPU usage on {server_id} is {current_metrics['cpu_usage_percent']}% (above 90% threshold).")
        
        anomaly_details = {
            "metric": "cpu_usage_percent",
            "value": current_metrics["cpu_usage_percent"],
            "timestamp": datetime.datetime.now()
        }
        
        # AI takes over: Assess the anomaly with rich context
        ai_result = assess_incident_with_context(server_id, anomaly_details)
        
        print(f"\n--- AI's Final Decision for {server_id} ---")
        print(f"  Assessment: {ai_result['assessment']}")
        print(f"  Severity: {ai_result['severity']}")
        print(f"  Recommendation: {ai_result['recommendation']}")
    else:
        print(f"  No immediate anomaly detected for {server_id}. Current CPU: {current_metrics.get('cpu_usage_percent', 'N/A')}% ")

if __name__ == "__main__":
    monitor_system("server-001")
