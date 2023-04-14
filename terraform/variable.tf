variable "node_count" {
  description = "The number of nodes in the GKE cluster"
  type = number
  default = 3
}
variable "machine_type" {
  description = "Machine type for nodes in the Kubernetes node pool"
  type        = string
  default     = "e2-standard-2"
}
