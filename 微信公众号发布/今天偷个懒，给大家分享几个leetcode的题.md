# 今天偷个懒，分享几个leetcode的题，还有我拙劣的解法😂

tags: [#leetcode]

### 1. 两数之和

给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。

你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。

来源：力扣（LeetCode）

#### 示例:

```
给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]
```


各位小伙伴可以思考下解法，我的解法放在最后面了，题目链接：

https://leetcode-cn.com/problems/two-sum/

有兴趣的小伙伴们都去试试，这是我的提交历史：

![](https://gitee.com/sysker/picBed/raw/master/images/20200712081029.png)

### 2、整数反转

给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。

#### 示例 1:

```
输入: 123
输出: 321
```

####  示例 2:

```
输入: -123
输出: -321
```

#### 示例 3:

```
输入: 120
输出: 21
注意:
```

假设我们的环境只能存储得下 32 位的有符号整数，则其数值范围为 [−231,  231 − 1]。请根据这个假设，如果反转后整数溢出那么就返回 0。

题目链接：https://leetcode-cn.com/problems/reverse-integer/

这次提交的代码就比较菜了，提交记录：

![](https://gitee.com/sysker/picBed/raw/master/images/20200712081832.png)

### 3、回文数

判断一个整数是否是回文数。回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。

#### 示例 1:

```
输入: 121
输出: true
```

#### 示例 2:

```
输入: -121
输出: false
```

解释: 从左向右读, 为 -121 。 从右向左读, 为 121- 。因此它不是一个回文数。

#### 示例 3:

```
输入: 10
输出: false
```

解释: 从右向左读, 为 01 。因此它不是一个回文数。

#### 进阶:

你能不将整数转为字符串来解决这个问题吗？

题目链接：https://leetcode-cn.com/problems/palindrome-number/

提交记录：

![](https://gitee.com/sysker/picBed/raw/master/images/20200712082249.png)

### 4、最长公共前缀

编写一个函数来查找字符串数组中的最长公共前缀。

如果不存在公共前缀，返回空字符串 ""。

#### 示例 1:

```
输入: ["flower","flow","flight"]
输出: "fl"
```

#### 示例 2:

```
输入: ["dog","racecar","car"]
输出: ""
```

解释: 输入不存在公共前缀。

#### 说明:

所有输入只包含小写字母 a-z 。

题目链接：https://leetcode-cn.com/problems/longest-common-prefix/

提交记录：

![](https://gitee.com/sysker/picBed/raw/master/images/20200712082628.png)

好了，废话少说，show me code:

#### 第一题

```java
 public int[] twoSum(int[] nums, int target) {
        int[] result = new int[2];
        for(int i=0; i < nums.length; i++) {
            for(int j = i + 1; j < nums.length; j++) {
                if(nums[i] + nums[j] == target) {
                    result[0] = i;
                    result[1] = j;
                    return result;
                }
                
            }
        }
        return result;
    }
```

#### 第二题

```java
public int reverse(int x) {
        String numStr = Integer.toString(x);       
        try {
            if(x < 0) {
                return Integer.parseInt(reverse(numStr));
            }
            return Integer.parseInt(reverse(numStr));
        }catch (NumberFormatException e) {           
        }
         return 0;
      
    }

    private String reverse(String str) {
        if(str.startsWith("-")) {
            return "-" + new StringBuffer(str.substring(1)).reverse().toString();
        }
        return new StringBuffer(str).reverse().toString();
    }
```

#### 第三题

```java
private String reverse(String str) {
        if(str.startsWith("-")) {
            return "-" + new StringBuffer(str.substring(1)).reverse().toString();
        }
        return new StringBuffer(str).reverse().toString();
    }

    public boolean isPalindrome(int x) {
        if(x < 0) {
            return false;
        }
        String xStr = Integer.toString(x);
        return reverse(xStr).equals(xStr);
    }
```

#### 第四题

```java
public String longestCommonPrefix(String[] strs) {
        if(strs == null || strs.length == 0) {
            return "";
        }
        String str = strs[0];
        if(strs.length == 1 ) {
            return str;
        }
        int length = str.length();
        String[] strs1 = Arrays.copyOfRange(strs, 1, strs.length);
        for (int i = length; i >= 1; i--) {
            String substring = str.substring(0, i);
            if (equalAllStr(substring, strs1)) {
                return substring;
            }
        }
        return "";
    }

    private boolean equalAllStr(String preFix, String[] strs) {
        for (String str : strs) {
            if (!str.startsWith(preFix)) {
                return false;
            }
        }
        return true;
    }
```

好了，今天就到这里，周末愉快呀！