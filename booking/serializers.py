from .models import RoomSubCategory, RoomCategory
from rest_framework import serializers

class RoomSubCategorySerializer(serializers.HyperlinkedModelSerializer):    
    category_id = serializers.CharField(source='category_id.id')    
    class Meta:
        model = RoomSubCategory    
        fields = '__all__'

class RoomCategorySerializer(serializers.HyperlinkedModelSerializer):
    subcategories = RoomSubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = RoomCategory
        fields = ('name', 'subcategories') 