import report  

def main(field_coordinates, obstacles, resolution):
    report.run_project(field_coordinates, obstacles, resolution)


if __name__ == "__main__":

    #EXAMPLE
    initial_point = (40.32897891010581, -8.653877052022354) # IN WGS 84 system
    second_point = (40.32879283914316, -8.654454588726981)
    third_point = (40.32871683817989, -8.654719293049935)
    fourth_point = (40.328673596214294, -8.654879146959251)
    fith_point = (40.328566146359954, -8.655171353054081)
    six_point = (40.328555374264695, -8.655347460383402)
    seventh_point = (40.32846503629598, -8.655627046067496)
    eigth_point = (40.32840434040056, -8.655762210033197)
    nineth_point = (40.32836340593132, -8.655858491213378)
    tenth_point = (40.328223663937365, -8.655725178834208)
    eleventh_point = (40.328280125383884, -8.655480772805728)
    twelve_point = (40.32830976762442, -8.655345608865737)
    thitennrd_point = (40.328380344335166, -8.654999366992056)
    fourtennth_point = (40.32850032457668, -8.654419828401345)
    fitennth_point = (40.32860901237369, -8.653973602243287)
    sixtennth_point = (40.328704996258885, -8.653592180685843)
    seventennth_point = (40.328875790774305, -8.653744008662159)

    field_coordinates = [
        initial_point, second_point, third_point, fourth_point, fith_point, six_point,
        seventh_point, eigth_point, nineth_point, tenth_point, eleventh_point,
        twelve_point, thitennrd_point, fourtennth_point, fitennth_point,
        sixtennth_point, seventennth_point
    ]

    obstacles = [
        {"format_type": "circle", "coordinates": (40.32850461030154, -8.654941160992928), "radius": 20},
        {"format_type": "rectangle", "coordinates":[(40.32837061698832, -8.655566710222692), (40.32835221399679, -8.655566710222692), (40.328340456527314, -8.655659246429018), (40.32837317295898, -8.655665281398996)], "radius": None}
    ]
    main(field_coordinates, obstacles, resolution=10)