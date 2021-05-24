docker-compose.yml

```yaml
version: "2"

services:
  sonarqube:
    image: sonarqube:6.7.1
    restart: always
    ports:
      - "9000:9000"
    depends_on:
      - db
    networks:
      - sonarnet
    environment:
      - sonar.jdbc.username=sonar
      - sonar.jdbc.password=sonar123
      - sonar.jdbc.url=jdbc:postgresql://db:5432/sonarqube
      - SONARQUBE_JDBC_USERNAME=sonar
      - SONARQUBE_JDBC_PASSWORD=sonar123
      - SONARQUBE_JDBC_URL=jdbc:postgresql://db:5432/sonarqube
    volumes:
      - /srv/docker/sonarqube/sonarqube_conf:/opt/sonarqube/conf
      - /srv/docker/sonarqube/sonarqube_data:/opt/sonarqube/data
      - /srv/docker/sonarqube/sonarqube_extensions:/opt/sonarqube/extensions

  db:
    image: postgres:9.6
    restart: always
    networks:
      - sonarnet
    environment:
      - POSTGRES_USER=sonar
      - POSTGRES_PASSWORD=sonar123
      - POSTGRES_DB=sonarqube
    volumes:
      - /srv/docker/sonarqube/postgresql:/var/lib/postgresql
      - /srv/docker/sonarqube/postgresql_data:/var/lib/postgresql/data

networks:
  sonarnet:
    driver: bridge
```

