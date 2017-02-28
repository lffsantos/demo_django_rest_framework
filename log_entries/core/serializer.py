from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from log_entries.core.models import Event, Category


class CategorySerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'name': instance.name
        }


class EventSerializer(serializers.BaseSerializer):

    def to_internal_value(self, data):
        note = data.get('note')
        end_date = data.get('end_date')
        start_date = data.get('start_date')
        category_id = data.get('category_id')
        user_id = data.get('user_id')

        # Perform the data validation.
        if not category_id:
            raise ValidationError({
                'category': 'This field is required.'
            })
        else:
            try:
                Category.objects.get(pk=category_id)
            except ObjectDoesNotExist:
                raise ValidationError({
                    'category': 'Invalid Category'
                })
        if not start_date:
            raise ValidationError({
                'start_date': 'This field is required.'
            })
        if len(note) > 255:
            raise ValidationError({
                'note': 'May not be more than 255 characters.'
            })

        data = {
            'note': note,
            'start_date': start_date,
            'category_id': category_id,
            'user_id': user_id,
        }
        if end_date:
            data['end_date'] = end_date

        return data

    def to_representation(self, instance):
        return {
            'start_date': instance.start_date,
            'end_date': instance.end_date,
            'note': instance.note,
            'category': instance.category.serialize
        }

    def create(self, validated_data):
        print(validated_data)
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.note = validated_data.get('note', instance.note)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.save()
        return instance


class UserSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        return {
            'full_name': instance.first_name + ' ' + instance.last_name
        }