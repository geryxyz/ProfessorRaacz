import pytest
from app import *


def main():
    print(sys.argv[8])
    pytest.main(['--html=./reports/report.html' , 'static/'+sys.argv[8]])

if __name__ == '__main__':
    main()