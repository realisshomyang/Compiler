# Compiler

## 프로젝트 설명

이 프로젝트는 중앙대학교 23-1학기 compiler term project의 코드와 테스트 파일을 저장해놓은 repository입니다 :) 

simple JAVA CFG에 대한 parsing 가능 여부를 파악하고, 파스 트리를 제공해줍니다. 


## 설치 안내

### Needs for running

```bash
Python 3.6.9+
pip (package installer for Python)
graphviz(visualize parse tree)
platform : Linux(ubuntu)
```

### Installation

```bash\
sudo apt-get install python3-pip
sudo apt-get install graphviz
git clone https://github.com/realisshomyang/Compiler.git
cd Compiler
pip install -r requirements.txt
```

### running command

```bash\
if linux
python3 syntax_analyzer.py input.txt
if MAC OS
python3 syntax_analyzer_mac.py input.txt
```
