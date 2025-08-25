.source HLang.java
.class public HLang
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
.var 1 is a [I from Label0 to Label1
	iconst_2
	newarray int
	dup
	iconst_0
	bipush 10
	iastore
	dup
	iconst_1
	bipush 20
	iastore
	astore_1
.var 2 is b [I from Label0 to Label1
	aload_1
	invokevirtual [I/clone()Ljava/lang/Object;
	checkcast [I
	astore_2
	aload_2
	iconst_1
	iconst_2
	iastore
	ldc ""
	aload_2
	iconst_1
	iaload
	invokestatic io/int2str(I)Ljava/lang/String;
	invokevirtual java/lang/String/concat(Ljava/lang/String;)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	ldc ""
	aload_1
	iconst_1
	iaload
	invokestatic io/int2str(I)Ljava/lang/String;
	invokevirtual java/lang/String/concat(Ljava/lang/String;)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	return
Label1:
.limit stack 6
.limit locals 3
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
