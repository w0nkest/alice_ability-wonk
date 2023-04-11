import musicbrainzngs

artist_id = "c5c2ea1c-4bde-4f4d-bd0b-47b200bf99d6"
result = musicbrainzngs.get_artist_by_id(artist_id,
              includes=["release-groups"], release_type=["album", "ep"])
for release_group in result["artist"]["release-group-list"]:
    print("{title} ({type})".format(title=release_group["title"],
                                    type=release_group["type"]))