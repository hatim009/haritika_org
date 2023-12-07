import json

from rest_framework import serializers
from rest_framework.fields import empty

from land_parcels.models import LandParcelPicture
from files_manager.serializers import FileSerializer


class LandParcelPictureListSerializer(serializers.ListSerializer):      
    """
    There is a bug in rest_framework.serializers.ListSerializer.get_field() where 
        "if html.is_html_input(dictionary):" on line 604
    returns True for non-html input, hence need to override.
    """
    def get_value(self, dictionary):
        return dictionary.get(self.field_name, empty)

    def to_internal_value(self, data):
        internal_data = [ {'picture': picture, 'instance': self.picture_instances[picture['id']]} if picture.get('id') and picture['id'] in self.picture_instances else {'picture': picture}  for picture in json.loads(data)]
        return super().to_internal_value(internal_data)

    def set_instance(self, land_parcel, land_parcel_pictures):
        self.land_parcel = land_parcel
        self.picture_instances = {land_parcel_picture.picture.id:land_parcel_picture.picture for land_parcel_picture in land_parcel_pictures}

    def create(self, land_parcel, pictures):     
        pictures = self.child.create(pictures)
        land_parcel_pictures = [LandParcelPicture(land_parcel=land_parcel, picture=picture) for picture in pictures]
        return LandParcelPicture.objects.bulk_create(land_parcel_pictures)

    def update(self, land_parcel_pictures, pictures):
        updated_pictures = self.child.update(self.picture_instances, pictures)
        
        current_picture_ids = [land_parcel_picture.picture.id for land_parcel_picture in land_parcel_pictures]
        updated_picture_ids = [picture.id for picture in updated_pictures]

        existing_land_parcel_pictures = [land_parcel_picture for land_parcel_picture in land_parcel_pictures if land_parcel_picture.picture.id in updated_picture_ids]
        
        # Since we have set LandParcelPicture.picture to on_delete=models.CASCADE no need to delete the removed entries explicitly
        removed_land_parcel_pictures = [land_parcel_picture for land_parcel_picture in land_parcel_pictures if land_parcel_picture.picture.id not in updated_picture_ids]

        new_land_parcel_pictures = [LandParcelPicture(land_parcel=self.land_parcel, picture=picture) for picture in updated_pictures if picture.id not in current_picture_ids]

        return existing_land_parcel_pictures + LandParcelPicture.objects.bulk_create(new_land_parcel_pictures)


class LandParcelPictureSerializer(serializers.ModelSerializer):
    picture = FileSerializer()

    class Meta:
        model = LandParcelPicture
        fields = ['picture']
        depth = 2
        list_serializer_class = LandParcelPictureListSerializer

    def to_internal_value(self, data):
        self.fields['picture'].instance = data.pop('instance', None)
        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        return super().to_representation(instance)['picture']

    def create(self, pictures):
        return self.fields['picture'].bulk_create([picture['picture'] for picture in pictures])
    
    def update(self, picture_instances, validated_pictures):
        return self.fields['picture'].bulk_update(picture_instances, [picture['picture'] for picture in validated_pictures])