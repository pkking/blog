Title: Manacher 算法求最长回文子串
Tags: algrithm, manacher, palindromic, leetcode
Date: 2017-07-31 19:58

# 背景
本文来源于`leetcode`上的一道求最长回文子串的[中级算法题](https://leetcode.com/problems/longest-palindromic-substring)
## 先来个思路
在给定的字符串中，要求出最长的回文子串，首先想到的，就是遍历字符串，将其中的回文串找出来，然后求出最长的串
然而根据排列组合，长度为`n`的字符串，其子串个数为`O(n^2)`数量级，因此该思路的时间复杂度至少也是`O(n^2)`

