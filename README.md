# Fast and tiny: raytracing in python

![](https://raw.githubusercontent.com/ssloy/fast-and-tiny/main/result.png)

Who said that the code in this repository is fast **and** tiny? :)

Here are two versions: [tiny.py](https://github.com/ssloy/fast-and-tiny/blob/main/tiny.py) in 62 lines of code, very easy to read, but pretty slow. The other one, [fast.py](https://github.com/ssloy/fast-and-tiny/blob/main/fast.py) is a bit harder to read, but it is orders of magnitude faster.

# tiny.py: how it works (writing in progress)

```
for each pixel
  compute color
```

![](https://raw.githubusercontent.com/ssloy/fast-and-tiny/46542e64039381dee9a693781fa314d58de873b1/result.png)

```
for each pixel
  emit a ray from the origin trough the pixel
  if the ray intersects the sphere
    paint sphere color
  else
    paint background
```

![](https://raw.githubusercontent.com/ssloy/fast-and-tiny/97ee4ca6cc9279bd21b4d0d392c2c31e58da90b7/result.png)

```
for each pixel
  emit a ray from the origin trough the pixel
  for all objects in the scene
    select the frontmost intersection point
  if the ray intersects the scene
    paint intersection point color
  else
    paint background
```

![](https://raw.githubusercontent.com/ssloy/fast-and-tiny/3a3571f4c829576d4c256125064033bf8aef6c6a/result.png)

![](https://raw.githubusercontent.com/ssloy/fast-and-tiny/09f957b4f4112f5a2e502e6f1bfa445ad73aa83c/result.png)

```
for each pixel
  emit a ray from the origin trough the pixel
  for all objects in the scene
    select the frontmost intersection point
  if the ray intersects the scene
    recursively emit a reflected ray
    cumulate colors through reflexions
  else
    paint background
```


![](https://raw.githubusercontent.com/ssloy/fast-and-tiny/37088b33a3e1ce68d86e4e6097408a2d9b3b0838/result.png)

![](https://raw.githubusercontent.com/ssloy/fast-and-tiny/721b67309ab24998d870fcd0a3a8e8c04edfb680/result.png)

# fast.py: how it works (writing in progress)
