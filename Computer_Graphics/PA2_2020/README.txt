1. 추가한 전역변수
1) currentPos : 현재 마우스 커서의 위치를 담은 변수입니다. 
2) select : 롤러코스터가 끝났을때 시작지점을 initial point 로 하기 위한 값 또는 V_DRAG 와 H_DRAG의 동기화를 위한 값이 저장돼있습니다.
3) save  : V_DRAG에서 H_DRAG, H_DRAG에서 V_DARG로 넘어갈 때의 PickInfo를 저장하여 동기화합니다.
4) save2 : 롤러코스터가 끝난 후 array[1]을 initial point로 해줍니다.
5) start : glfw.get_time()으로 시간을 받아와 0부터 시작합니다.
6) mode : control point를 만들 때 0이고 소가 움직일 때 1인 값으로, display 모드를 결정합니다.
7) array : control point 로 정한곳의 cow2wld를 저장하기 위한 배열입니다.
8) index : 7)array를 저장하기 위한 index값 입니다.

2. 추가된 함수

1) CMR(t) : 캣멀롬 spline을 구현한 함수로 시간 t를 입력 받아 변화된 cow2wld 를 반환 합니다.
M에 translation을 저장하고 fM에 cow의 face방향에 대한 정보를 저장합니다.
M1,M2에 rotation 정보를 저장하여 M에 새로운 cow2wld 값을 저장하여 반환합니다.

2) display2 : cow2wld를 업데이트해서 보여주는 곳으로 display 말고 이부분에서 보여줍니다. 
CMR(t)에서 반환한 cow2wld 값을 drawCow를 사용하여 그립니다.

3. 변경된 함수
1)onMouseButton : mouse down에서 array에 cow2wld를 저장합니다.
2)onMouseDrag: 수직으로 움직일 때 x값과 z값은 고정하고 y값만 변할수 있게 만듭니다.
3)main : mode가 0일 때 control point를 입력하고 mode가 1이라면 롤러코스터를 보여줍니다.

