from rest_framework import serializers


class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    id = serializers.IntegerField(read_only=True)
    btitle = serializers.CharField(max_length=20)
    bpub_date = serializers.DateField()
    bread = serializers.IntegerField()
    bcomment = serializers.IntegerField()
    image = serializers.ImageField()
