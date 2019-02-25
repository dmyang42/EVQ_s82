```
python s82_gband.py tar > EVQ_list
```

tar可改为ftr, oth, tar代表生成EVQ的一组list。list含有的参数可以改，起初为了做找与EVQ红移、光度、质量match的一组sample要生成包含这些参数的list(/list/s82_tar)，然后执行以下命令：

```shell
python gen_match.py 0.1
```

这样会得到一组match的sample，最后整理一下是以下两组lists:

- ``./list/EVQ_list``

- ``./list/match_list``

然后执行：

```bash
python gen_delta.py EVQ i > delta_EVQ_i
```

```bash
python gen_delta.py match i > delta_match_i
```

i = 1, 2, 3, 4, 5 $\Rightarrow$ u, g, r, i, z

```bash
python gen_bin.py n i
```

n = 2, 3, 4, 5 … 代表分bin数目, i同上

上面的指令首先是按照时延和对应光变幅度生成临时文件(/cache/)，然后做bootstrap计算。



