resource "google_container_node_pool" "general" {
  name       = "general"
  location   = "us-central1-a"
  cluster    = google_container_cluster.main.name
  node_count = var.node_count

  node_config {
    machine_type = var.machine_type
    service_account = google_service_account.kubernetes_node.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}
