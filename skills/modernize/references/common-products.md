# Common Products Reference

## Operating Systems

| Product ID       | Description              |
|------------------|--------------------------|
| `ubuntu`         | Ubuntu Linux             |
| `debian`         | Debian Linux             |
| `rhel`           | Red Hat Enterprise Linux |
| `centos`         | CentOS                   |
| `centos-stream`  | CentOS Stream            |
| `rocky-linux`    | Rocky Linux              |
| `almalinux`      | AlmaLinux                |
| `amazon-linux`   | Amazon Linux             |
| `oracle-linux`   | Oracle Linux             |
| `fedora`         | Fedora                   |
| `opensuse`       | openSUSE                 |
| `alpine`         | Alpine Linux             |
| `macos`          | macOS                    |
| `windows`        | Microsoft Windows        |
| `windows-server` | Windows Server           |

## Programming Languages & Runtimes

| Product ID | Description   |
|------------|---------------|
| `ruby`     | Ruby          |
| `python`   | Python        |
| `nodejs`   | Node.js       |
| `go`       | Go            |
| `java`     | Java (Oracle) |
| `openjdk`  | OpenJDK       |
| `dotnet`   | .NET          |
| `php`      | PHP           |
| `rust`     | Rust          |
| `perl`     | Perl          |

## Databases

| Product ID      | Description   |
|-----------------|---------------|
| `postgresql`    | PostgreSQL    |
| `mysql`         | MySQL         |
| `mariadb`       | MariaDB       |
| `mongodb`       | MongoDB       |
| `redis`         | Redis         |
| `elasticsearch` | Elasticsearch |
| `sqlite`        | SQLite        |

## Web Servers & Proxies

| Product ID | Description        |
|------------|--------------------|
| `nginx`    | NGINX              |
| `apache`   | Apache HTTP Server |
| `haproxy`  | HAProxy            |
| `traefik`  | Traefik            |
| `tomcat`   | Apache Tomcat      |

## Configuration Management & DevOps

| Product ID          | Description       |
|---------------------|-------------------|
| `chef-infra-client` | Chef Infra Client |
| `chef-infra-server` | Chef Infra Server |
| `ansible`           | Ansible           |
| `terraform`         | Terraform         |
| `kubernetes`        | Kubernetes        |
| `docker-engine`     | Docker Engine     |

## Atlassian Products

| Product ID      | Description          |
|-----------------|----------------------|
| `confluence`    | Atlassian Confluence |
| `jira-software` | Jira Software        |
| `bitbucket`     | Bitbucket            |

## Cloud Platforms

| Product ID                 | Description              |
|----------------------------|--------------------------|
| `amazon-eks`               | Amazon EKS               |
| `azure-kubernetes-service` | Azure Kubernetes Service |
| `google-kubernetes-engine` | Google Kubernetes Engine |

## API Endpoints

```text
Base URL: https://endoflife.date/api/v1

GET /products                     - List all products
GET /products/{product}           - Get product details with all releases
GET /products/{product}/releases/latest - Get latest release
GET /products/{product}/releases/{cycle} - Get specific release cycle
GET /categories                   - List categories
GET /categories/{category}        - Products in category
```

## Response Fields

Key fields in release cycle responses:

- `name` - Release cycle name (e.g., "22.04")
- `releaseDate` - Initial release date
- `isEol` - Whether cycle is end-of-life
- `eolFrom` - EOL date
- `isLts` - Whether it's an LTS release
- `latest.name` - Latest patch version
- `isMaintained` - Whether still receiving updates
