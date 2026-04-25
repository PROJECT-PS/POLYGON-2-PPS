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

`<pps_package_path>`는 새로 생성될 PPS Package의 경로입니다. Polygon2PPS에서 자동으로 폴더를 생성해주기 때문에 폴더를 생성하지 않고 실행해도 무방합니다. **단, 기존 폴더 내에 파일이 존재하는 경우, 이름이 같은 파일은 덮어쓰고, 그 외 파일은 그대로 유지됩니다.**

빈 템플릿으로 PPS Package(문제)를 생성한 후, 비어있는 Repository를 Clone 받은 후 해당 폴더를 `<pps_package_path>`로 지정하여 실행하는 것을 강력히 권장드립니다.

## Difference beteween Polygon and PPS

* 현재 latex to markdown 변환을 지원하고 있습니다. 다만, 완벽하지 않기 때문에, 변환이 올바르게 됐는지 확인해야 합니다.
* PPS에서는 테스트케이스를 매뉴얼하게 생성하는 방법을 지원하지 않습니다.
    * **따라서, 메뉴얼한 테스트케이스를 생성하는 제네레이터를 자동으로 생성해줍니다.** 다만, 사이즈가 커지는 경우, 웹에서 확인이 안 될 수 있습니다.
* 폴리곤에서 제네레이터 이름에 공백이 들어갈 수 있는지는 모르겠으나, 들어간 경우 문제가 발생합니다.
* 지문에 포함되는 사진 파일은 옮겨지지 않습니다. 별도 사진 업로드 시스템을 활용해야 합니다.
* 헤더 파일을 추가해놓고 여러 코드에서 사용하는 기능이 PPS에 존재하지 않습니다. 이 경우, 헤더 파일을 사용하는 모든 파일을 직접 수정해야 합니다.

## TODO

* ~~Statement Auto Compiling Tex to Markdwon~~
* Statement Auto Compiling Tex to Markdown For General Case (Not Tested Properly)
