from anal_poses.utils import p3_angle
from anal_poses.utils import p2_diff
from anal_poses.utils import add_korean_keyword
# from anal_poses.utils import key_to_str


# 5번 자세
class Impact:
    def __init__(self, kp, face_on=True):
        self.kp = kp
        self.face_on = face_on
        self.feedback = dict()

    def sway(self):
        lshoulder = self.kp[5][5]
        lfoot = self.kp[5][14]
        height = self.kp[0][1][1] - self.kp[0][11][1]

        diff = p2_diff(lshoulder, lfoot) / height

        if diff[0] <= 0.2:
            self.feedback["sway"] = {
                0: 2,
                1: diff[0],
                2: "스웨이 체크"
            }
        elif diff[0] <= 0.3:
            self.feedback["sway"] = {
                0: 1,
                1: diff[0],
                2: "체중 이동 시 상체가 좌우로 움직이고 있습니다. 정확한 임팩트가 어렵고 거리 손실을 보게 됩니다. "
            }
        else:
            self.feedback["sway"] = {
                0: 0,
                1: diff[0],
                2: "체중 이동 시 상체가 좌우로 움직이고 있습니다. 정확한 임팩트가 어렵고 거리 손실을 보게 됩니다. "
            }


    def reverse_pivot(self):
        lshoulder = self.kp[5][5]
        lfoot = self.kp[5][14]
        height = self.kp[0][1][1] - self.kp[0][11][1]

        diff = p2_diff(lshoulder, lfoot) / height

        if 0.05 <= diff[0]:
            self.feedback["reverse_pivot"] = {
                0: 2,
                1: diff[0],
                2: "리버스 피벗 체크"
            }
        elif 0.0 <= diff[0]:
            self.feedback["reverse_pivot"] = {
                0: 1,
                1: diff[0],
                2: "임팩트 시 무게 중심이 아직 오른발에 있는지 확인해보세요."
            }
        else:
            self.feedback["reverse_pivot"] = {
                0: 0,
                1: diff[0],
                2: "임팩트 시 무게 중심이 아직 오른발에 있는지 확인해보세요."
            }

    def wrist_lead_club(self):
        lwrist = self.kp[5][7]
        club = self.kp[5][25]
        height = self.kp[0][1][1] - self.kp[0][11][1]

        diff = p2_diff(lwrist, club)[0] / height

        if 0 <= diff:
            self.feedback["wrist_lead_club"] = {
                0: 2,
                1: diff,
                2: "래깅"
            }
        elif -0.5 <= diff:
            self.feedback["wrist_lead_club"] = {
                0: 1,
                1: diff,
                2: "다운 스윙에서부터 끌고온 래깅이 임팩트까지 유지되는 것이 좋습니다."
            }
        else:
            self.feedback["wrist_lead_club"] = {
                0: 0,
                1: diff,
                2: "다운 스윙에서부터 끌고온 래깅이 임팩트까지 유지되는 것이 좋습니다."
            }

    def head_position(self):
        nose_address = self.kp[0][0]
        nose_impact = self.kp[5][0]
        height = self.kp[0][1][1] - self.kp[0][11][1]

        diff = p2_diff(nose_address, nose_impact)[1] / height

        if -0.15 <= diff <= 0.2:
            self.feedback["head_position"] = {
                0: 2,
                1: diff,
                2: "헤드 포지션"
            }
        elif -0.5 <= diff <= 0.5:
            self.feedback["head_position"] = {
                0: 1,
                1: diff,
                2: "머리가 상하로 움직이면 일관된 스윙 궤도를 얻기 힘들어집니다."
            }
        else:
            self.feedback["head_position"] = {
                0: 0,
                1: diff,
                2: "머리가 상하로 움직이면 일관된 스윙 궤도를 얻기 힘들어집니다."
            }


    def run(self):
        if self.face_on:
            self.sway()
            self.reverse_pivot()
            self.wrist_lead_club()
            self.head_position()

        # 결과 인덱스 3번에 한국어 간단 설명 추가
        add_korean_keyword(self.feedback, KOREAN_KEYWORD)

        # 모든 키를 스트링으로 바꾼 결과 리턴
        # return key_to_str(self.feedback)
        return self.feedback


KOREAN_KEYWORD = {
    "sway": "스웨이",
    "wrist_lead_club": "래깅 유지",
    "reverse_pivot": "역피봇",
    "head_position": "헤드 포지션",
    "head": "임팩트시 머리의 위치",
    "back_angle": "백스윙때의 척추의 각도와 임팩트시 척추의 각도",
}