import os
from pathlib import Path
import numpy as np
from PIL import Image

def cut_webtoon_simple(img: Image.Image,
                       out_dir: str = "./cap_img",
                       min_panel_h: int = 200,
                       pad: int = 0) -> int:
    """
    웹툰 세로 스크롤 이미지를 컷 단위로 잘라 저장
    """
    gray = np.array(img.convert("L")) # 원활한 전처리를 위해 gray scale로 전환. (어짜피 회색조여도 컬러의 차이는 반영이 되니까.)
    mask = (gray != gray[:, 0][:, None]).any(axis=1) # 이미지의 로우단 스칼라값이 모두 같은 경우, 해당 칸은 이미지가 없는 칸으로 간주, cut라인으로 잡음
    idx = np.flatnonzero(mask)

    if idx.size == 0:
        print("[정보] 내용 있는 행을 찾지 못했습니다.")
        return 0

    starts = [max(0, idx[0] - 1)]
    ends = []
    for i in range(len(idx) - 1):
        if idx[i + 1] != idx[i] + 1:
            ends.append(min(img.height, idx[i] + 1))
            starts.append(max(0, idx[i + 1] - 1))
    ends.append(min(img.height, idx[-1]))

    segments = [] # crop된 이미지의 세로 길이가 200픽셀을 넘어가지 않을 경우 해당 이미지의 start, end line이 튜플 형태로 등록됨
    for s, e in zip(starts, ends):
        top = max(0, s - pad)
        bottom = min(img.height, e + pad)
        if bottom - top >= min_panel_h:
            segments.append((top, bottom))

    if not segments:
        print("[정보] 조건(min_panel_h) 충족하는 패널이 없습니다.")
        return 0


    # crop을 한 이미지를 보관하는 파일 추가
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    def next_png_path(name: str) -> Path:
        p = out_dir / f"{name}.png"
        if not p.exists():
            return p
        n = 1
        while True:
            cand = out_dir / f"{name} ({n}).png"
            if not cand.exists():
                return cand
            n += 1

    saved = 0
    for i, (top, bottom) in enumerate(segments):
        crop = img.crop((0, top, img.width, bottom))
        path = next_png_path(str(i))
        crop.save(path.as_posix(), "PNG")
        saved += 1

    print(f"[완료] {saved}개 저장 → {out_dir}")
    return saved

if __name__ == "__main__":
    # 실행 예시
    image_path = input("이미지 파일 경로를 입력하세요: ").strip() # 터미널에 컷할 이미지 file path를 직접 작성. 
    if not os.path.exists(image_path):
        print("[오류] 파일이 존재하지 않습니다.") 
    else:
        img = Image.open(image_path).convert("RGB")
        base_name = Path(image_path).stem
        result_dir = f"./{base_name}_result"
        cut_webtoon_simple(img, out_dir=result_dir, min_panel_h=200, pad=0)