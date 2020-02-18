<img src="https://github.com/IKNL/guidelines/blob/master/resources/logos/vantage6.png?raw=true" width=200 align="right">

# Distributed Round Robin Test

|:warning: priVAcy preserviNg federaTed leArninG infrastructurE for Secure Insight eXchange (VANTAGE6) |
|------------------|
| This algorithm is part of [VANTAGE6](https://github.com/IKNL/VANTAGE6). A docker build of this algorithm can be obtained from docker-registry.distributedlearning.ai/droundrobintest |

Algorithm that tests/demonstrates vertical tasks. Each node reports its (unique) id to the server. The nodes report their id's in Round Robin style (in consecutive tasks).

## Possible Privacy Issues

None

## Privacy Protection

✔️ Only the `id` of the node of the organization is reported

✔️ Database is not mounted (or read in any other way)

## Input.txt
### master
```
{
  "method": "master"
}
```

### my_turn
```
{
  "method": "my_turn"
}
```

## Test / Develop

You need to have Docker installed.

To Build (assuming you are in the project-directory):
```
docker build -t droundrobintest .
```

To test/run the node-algorithm `my_turn` locally the folder `local` is included in the repository. The following command should run the algorithm.
```
docker run -v .\local\my_turn\input.txt:/app/input.txt -v .\local\my_turn\token.txt:/app/token.txt -v .\local\my_turn\output.txt:/app/output.txt droundrobintest
```
