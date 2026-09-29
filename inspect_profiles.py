try:
    import langchain_model_profiles

    print(dir(langchain_model_profiles))
    print(langchain_model_profiles.__file__)
except ImportError:
    print("langchain-model-profiles not installed")
