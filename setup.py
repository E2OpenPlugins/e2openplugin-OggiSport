from distutils.core import setup, Extension

pkg = 'Extensions.OggiSport'
setup (name='enigma2-plugin-extensions-oggisport',
       version='0.1',
       license='GPLv2',
       url='https://github.com/E2OpenPlugins',
       description='OggiSport',
       long_description='Lo Sport di oggi in Tv',
       author='meo',
       author_email='lupomeo@hotmail.com',
       packages=[pkg],
       package_dir={pkg: 'plugin'},
       package_data={pkg: ['*.png']}
      )
