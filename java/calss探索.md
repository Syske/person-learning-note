### 常用方法

#### getName()方法

<blockquote><table summary="Element types and encodings">
    <tr><th align=center> Element Type </th> &nbsp;&nbsp;&nbsp; <th align=center> Encoding</th></tr>
    <tr><td align=center> boolean      </td> &nbsp;&nbsp;&nbsp; <td align=center> Z</td></tr>
    <tr><td align=center> byte         </td> &nbsp;&nbsp;&nbsp; <td align=center> B</td></tr>
    <tr><td align=center> char         </td> &nbsp;&nbsp;&nbsp; <td align=center> C</td>
    <tr><td align=center> class or interface</td>
      &nbsp;&nbsp;&nbsp; <td align=center> L<i>classname</i>;</td></tr>
<tr><td align=center> double       </td> &nbsp;&nbsp;&nbsp; <td align=center> D</td></tr>
<tr><td align=center> float        </td> &nbsp;&nbsp;&nbsp; <td align=center> F</td></tr>
<tr><td align=center> int          </td> &nbsp;&nbsp;&nbsp; <td align=center> I</td></tr>
<tr><td align=center> long         </td> &nbsp;&nbsp;&nbsp; <td align=center> J</td></tr>
<tr><td align=center> short        </td> &nbsp;&nbsp;&nbsp; <td align=center> S</td></tr>
</table></blockquote>

**注意：**对于数组，该方法获取到的值为[[[Ljava.lang.Object，其中[表示数组，[的数量表示数组的维度，一维数组一个，二位数组为两个，如上显示的时三维数组