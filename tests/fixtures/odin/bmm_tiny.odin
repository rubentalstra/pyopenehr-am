<
    model_name = <"TINY_RM">

    packages = <
        ["rm"] = <
            name = <"rm">

            classes = <
                ["DV_TEXT"] = <
                    properties = <
                        ["value"] = <
                            type = <"String">
                            multiplicity = < lower = <1>; upper = <1> >
                        >

                        ["mappings"] = <
                            type = < name = <"LIST">; parameters = <"String"> >
                            multiplicity = < lower = <0>; upper = <"*"> >
                            ignored_field = <"ignored">
                        >
                    >
                >
            >
        >
    >
>
