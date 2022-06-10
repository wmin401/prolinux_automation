# 데몬 자동화 검증 방법
##### 1. Jenkins에서 PRE_CONDITION 항목 체크
##### 2. Jeknins에서 daemon_all.txt에 대해 검증 수행
##### 3. Host 컴퓨터 재부팅 후 다른 검증 수행

# 파일별 성명
- daemon_all.txt : 모든 데몬 파일이 포함된 리스트
- daemon_for_precondition.txt : 사전 조건 충족이 필요한 데몬 리스트
- daemon_skip.txt : 자동화 검증에서 제외된 데몬 리스트
- 별도로 테스트 후 자동화 가능 시 daemon_skip.txt에서 제외하고 daemon_all.txt에 포함시킴
- test_* : 개인용 테스트 파일
# 주의 사항
daemon_for_pre_condition.txt에서는 인자를 제외하고 리스트를 포함시키 daemon_all.txt에서는 인자를 같이 넣어 리스트를 생성함
예시)
- daemon_all.txt : /usr/lib/systemd/system/chrony-dnssrv@**_ntp._udp.test**.service
- daemon_for_pre_condition.txt : /usr/lib/systemd/system/chrony-dnssrv@.service
