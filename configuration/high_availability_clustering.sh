#!/bin/bash

echo "HA 설정 (OracleLinux 8.1 기준)"

echo "레포 추가"
dnf config-manager --enable ol8_appstream ol8_baseos_latest ol8_addons

echo "패키지 설치"
dnf install -y pcs pacemaker resource-agents fence-agents-all

echo "방화벽 서비스로 HA 등록"
firewall-cmd --add-service=high-availability

echo "HA cluster용 비밀번호 설정"
passwd hacluster

echo "pcs 데몬 활성화"
systemctl enable --now pcsd.service

echo "/etc/hosts 아래 노드 추가(IP에 따라 사용자 정의 설정 가능)"
echo "192.168.17.38 node1" >> /etc/hosts
echo "192.168.17.123 node2" >> /etc/hosts

echo "node 설정(이름: node1), 비밀 번호 입력"
yes "asdf" | pcs host auth node1 node2 -u hacluster

echo "클러스터 생성"
pcs cluster setup pacemaker1 node1 node2

echo "클러스터 모두 시작"
pcs cluster start --all
# systemctl start pacemaker.service

echo "부팅 시 모든 클러스터 자동 시작 설정"
pcs cluster enable --all
# systemctl enable pacemaker.service

echo "펜싱 기능 비활성화"
pcs property set stonith-enabled=false

echo "쿼럼 상태를 무시하도록 클러스터를 구성"
pcs property set no-quorum-policy=ignore

echo "마이그레이션 정책 구성(기본값)"
pcs resource defaults migration-threshold=1
# Warning: Defaults do not apply to resources which override them with their own defined values
# 경고 : 기본값은 자체 정의 된 값으로 재정의하는 리소스에는 적용되지 않습니다.
# 단일 장애 후 서비스를 새 노드로 이동하도록 클러스터가 구성
