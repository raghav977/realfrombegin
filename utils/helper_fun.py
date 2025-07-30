from classes.models import Class_section

def check_class_section_exist(class_obj,section_obj):
    
    class_section = Class_section.objects.filter(class_room=class_obj,section=section_obj).exists()
    
    if class_section is None:
        return False
    else:
        return True
    
    
    pass