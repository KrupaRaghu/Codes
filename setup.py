import setuptools

setuptools.setup(
    name='dreene_BA',
    setup_requires=["pbr"],
    pbr=True,
    packages=['pipelines', 'pipelines.classes', 'pipelines.scripts', 'pipelines.formats', 'pipelines.reduces', 'pipelines.maps']
)
