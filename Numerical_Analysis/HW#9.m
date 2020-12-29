ckI =imread('face.jpg');
red = I(:,:,1);
blue = I(:,:,2);
green = I(:,:,3);

red_img = im2double(red);
blue_img = im2double(blue);
green_img = im2double(green);

T = dctmtx(16);
dct = @(block_struct) T * block_struct.data * T';

B_R = blockproc(red_img,[16 16],dct);
B_B = blockproc(blue_img,[16 16],dct);
B_G = blockproc(green_img,[16 16],dct);

mask = [ 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
         1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
         1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0
         1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
         1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0];
     
B2_red = blockproc(B_R,[16 16],@(block_struct) mask .* block_struct.data);
B2_green = blockproc(B_G,[16 16],@(block_struct) mask .* block_struct.data);
B2_blue = blockproc(B_B,[16 16],@(block_struct) mask .* block_struct.data);

invdct = @(block_struct) T' * block_struct.data * T;

I2_red = blockproc(B2_red,[16 16],invdct);
I2_green = blockproc(B2_green,[16 16],invdct);
I2_blue = blockproc(B2_blue,[16 16],invdct);

rgbImage = cat(3, I2_red,I2_blue,I2_green);
imshow(rgbImage);
imwrite(rgbImage,'result.png');