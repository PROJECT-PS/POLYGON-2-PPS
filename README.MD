# Polygon 2 PPS

Polygon Package를 PPS Package로 만들어주는 파이썬 프로그램입니다.

현재 Polygon에서 제공하는 기능과 PPS에서 제공하는 기능의 차이점이 있어 완벽하게 변환할 수는 없습니다.

## Requirements

- Python 3.8+
- Polygon Pacakge (Linux Version)

## How to Use

처음 실행하는 경우 `requirements.txt`에 있는 라이브러리를 설치해야 합니다.

```
 $ pip3 install -r requirements.txt
```

`$ python3 run.py -h`를 사용하면 도움말을 볼 수 있습니다.

```
 $ python3 run.py -s <polygon_package_path> -d <pps_package_path>
```

`<pps_package_path>`는 새로 생성될 PPS Package의 경로입니다. Polygon2PPS에서 자동으로 폴더를 생성해주기 때문에 폴더를 생성하지 않고 실행해도 무방합니다.

## Difference beteween Polygon and PPS

* PPS에서는 STDIO 타입만 지원합니다.
* ~~PPS에서는 지문을 Markdown 형식으로 작성해야 하므로, Polygon에서 제공하는 지문은 파일은 옮겨주되 Markdown 형식으로 편집해야 합니다.~~
  * 현재 latex to markdown 변환을 지원하고 있습니다. 다만, 올바르게 변환됐는지 꼭 확인해야 합니다.
* PPS에서는 테스트케이스를 매뉴얼하게 생성하는 방법을 지원하지 않습니다.
    * **따라서, 메뉴얼한 테스트케이스를 생성하는 제네레이터를 자동으로 생성해줍니다.** 다만, 손으로 만든 데이터 크기 합이 큰 경우 문제가 발생할 수도 있습니다. 이 경우 데이터를 압축하거나, 임의로 제네레이터를 분할하는 등 작업을 거쳐야 합니다. 자세한 이슈는 PPS 이용 가이드를 참고해주세요.
* 폴리곤에서 제네레이터 이름에 공백이 들어갈 수 있는지는 모르겠으나, 들어간 경우 문제가 발생합니다.
* 지문에 포함되는 사진 파일 혹은 헤더 파일 등을 업로드 해놓고 코드에서 불러와서 쓰는 등 외부 파일은 현재는 지원하지 않습니다.

## TODO

* ~~Statement Auto Compiling Tex to Markdwon~~
* Statement Auto Compiling Tex to Markdown For General Case (Not Tested Properly)
