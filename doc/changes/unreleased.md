# Unreleased

Verification of the Python/Exasol version format of the config by adding a BaseConfig class. To Use:
    
    #Use
        Project_Config = BaseConfig()
    #modify
        Project_Config = BaseConfig(python_versions=["3.12"])
    #expand
        class ProjectConfig(BaseConfig):
            extra_data: list[str] = ["data"]

        Project_Config = ProjectConfig()

## Feature

#465: Create BaseConfig class