from sqlalchemy.orm import Session
from app.models.profile import Profile, ProfileTypeEnum


def seed_profiles(db: Session):
    """Seed the profiles table with initial data."""
    
    profiles_data = [
        {
            "id": 1,
            "type": ProfileTypeEnum.eternity,
            "description": "Perfil Eternity - Acesso completo e vitalício",
            "rule_activation": {
                "unlimited_access": True,
                "premium_features": True,
                "priority_support": True
            },
            "plan_price": 0,  # Vitalício
            "active": True
        },
        {
            "id": 2,
            "type": ProfileTypeEnum.infinity,
            "description": "Perfil Infinity - Acesso premium com recursos avançados",
            "rule_activation": {
                "unlimited_access": True,
                "premium_features": True,
                "priority_support": False,
                "monthly_limit": 1000
            },
            "plan_price": 99,
            "active": True
        },
        {
            "id": 3,
            "type": ProfileTypeEnum.admin,
            "description": "Perfil Admin - Acesso administrativo completo",
            "rule_activation": {
                "admin_access": True,
                "user_management": True,
                "system_settings": True,
                "analytics": True
            },
            "plan_price": 0,
            "active": True
        },
        {
            "id": 4,
            "type": ProfileTypeEnum.standalone_profile,
            "description": "Perfil Standalone - Acesso individual com prazo de expiração",
            "rule_activation": {
                "limited_access": True,
                "basic_features": True,
                "expiration_date": True
            },
            "plan_price": 29,
            "active": True
        }
    ]
    
    for profile_data in profiles_data:
        # Verificar se o perfil já existe
        existing_profile = db.query(Profile).filter(Profile.id == profile_data["id"]).first()
        
        if existing_profile:
            # Atualizar perfil existente
            for key, value in profile_data.items():
                setattr(existing_profile, key, value)
        else:
            # Criar novo perfil
            profile = Profile(**profile_data)
            db.add(profile)
    
    db.commit()
    print("Profiles seeded successfully!")


def get_profiles_data():
    """Retorna os dados dos perfis para uso em outros contextos."""
    return [
        {
            "id": 1,
            "type": "eternity",
            "description": "Perfil Eternity - Acesso completo e vitalício",
            "rule_activation": {
                "unlimited_access": True,
                "premium_features": True,
                "priority_support": True
            },
            "plan_price": 0,
            "active": True
        },
        {
            "id": 2,
            "type": "infinity",
            "description": "Perfil Infinity - Acesso premium com recursos avançados",
            "rule_activation": {
                "unlimited_access": True,
                "premium_features": True,
                "priority_support": False,
                "monthly_limit": 1000
            },
            "plan_price": 99,
            "active": True
        },
        {
            "id": 3,
            "type": "admin",
            "description": "Perfil Admin - Acesso administrativo completo",
            "rule_activation": {
                "admin_access": True,
                "user_management": True,
                "system_settings": True,
                "analytics": True
            },
            "plan_price": 0,
            "active": True
        },
        {
            "id": 4,
            "type": "standalone_profile",
            "description": "Perfil Standalone - Acesso individual com prazo de expiração",
            "rule_activation": {
                "limited_access": True,
                "basic_features": True,
                "expiration_date": True
            },
            "plan_price": 29,
            "active": True
        }
    ]
