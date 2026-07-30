# Cloud Computing Fundamentals

## Virtualization

Virtualization allows a single physical server to run multiple isolated virtual machines, each with its own operating system. A hypervisor is the software layer that creates and manages these virtual machines, allocating CPU, memory, and storage from the physical host. Type 1 hypervisors run directly on hardware, while Type 2 hypervisors run on top of a host operating system.

## Containers

Containers package an application together with its dependencies, but unlike virtual machines, they share the host machine's operating system kernel. This makes containers significantly lighter and faster to start than virtual machines, often launching in under a second. Docker is the most widely used containerization platform, and Kubernetes is the standard tool for orchestrating containers across a cluster of machines.

A container image is built in layers, where each layer represents a filesystem change. Layers are cached, so rebuilding an image after a small code change only requires rebuilding the layers after that change, not the entire image.

## Serverless Computing

Serverless computing lets developers run code without managing servers directly, with the cloud provider automatically handling scaling and infrastructure. Despite the name, servers are still involved, but they're fully abstracted away from the developer. AWS Lambda, Google Cloud Functions, and Cloudflare Workers are common serverless platforms.

Cold starts are a known drawback of serverless functions: when a function hasn't been invoked recently, the platform must initialize a new execution environment before running the code, adding noticeable latency to that first request.

## Auto-Scaling

Auto-scaling automatically adjusts the number of running server instances based on current demand. Horizontal scaling adds or removes entire server instances, while vertical scaling increases or decreases the resources of an existing instance, such as adding more CPU or memory. Most cloud providers support scaling policies based on metrics like CPU utilization or request queue length.

## Content Delivery Networks

A content delivery network, or CDN, caches copies of static content across servers distributed around the world, so users can retrieve data from a location physically closer to them. This significantly reduces latency compared to fetching content from a single origin server. CDNs are especially effective for images, videos, and other assets that don't change frequently.
