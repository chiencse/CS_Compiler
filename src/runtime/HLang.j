.source HLang.java
.class public HLang
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
.var 1 is arr [[Ljava/lang/String; from Label0 to Label1
	iconst_2
anewarray [Ljava/lang/String;
	dup
	iconst_0
	iconst_2
anewarray java/lang/String
	dup
	iconst_0
	ldc "a"
	aastore
	dup
	iconst_1
	ldc "b"
	aastore
	aastore
	dup
	iconst_1
	iconst_2
anewarray java/lang/String
	dup
	iconst_0
	ldc "c"
	aastore
	dup
	iconst_1
	ldc "d"
	aastore
	aastore
	astore_1
	aload_1
	iconst_1
	aaload
	iconst_0
	ldc "cd"
	aastore
	aload_1
	iconst_1
	aaload
	iconst_0
	aaload
	invokestatic io/print(Ljava/lang/String;)V
	return
Label1:
.limit stack 15
.limit locals 2
.end method

.method public <init>()V
.var 0 is this LHLang; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	return
Label1:
.limit stack 1
.limit locals 1
.end method
