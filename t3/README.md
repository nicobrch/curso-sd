# Tarea 3

```shell
docker compose up --build
```

```shell
docker exec -it hadoop bash
```

```shell
hdfs dfs -mkdir /user
```

```shell
hdfs dfs -mkdir /user/hduser
```

```shell
hdfs dfs -mkdir input
```

```shell
sudo chown -R hduser .
```

```shell
cd trabajo
```

```shell
hdfs dfs -put docs_1/*.txt input
```

```shell
hdfs dfs -put docs_2/*.txt input
```

```shell
hdfs dfs -ls input
```

```shell
mapred streaming -files mapper.py,reducer.py -input /user/hduser/input/*.txt -output hduser/outhadoop/ -mapper ./mapper.py -reducer ./reducer.py
```

```shell
hdfs dfs -get /user/hduser/hduser/outhadoop/ /home/hduser/trabajo
```