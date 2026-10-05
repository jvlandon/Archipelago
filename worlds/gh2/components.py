from worlds.LauncherComponents import Component, Type, components, launch

def run_client(*args:str) -> None:
    from .client import main
    launch(main, name="Guitar Hero II Client", args=args)

components.append(
    Component("Guitar Hero II Client",
              func=run_client,
              game_name = "Guitar Hero II",
              component_type=Type.CLIENT,
              supports_uri=True)

)