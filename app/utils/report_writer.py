from pathlib import Path


def save_report_txt(
    report,
    filename="research2_report.txt"
):

    output_dir = Path("reports")

    output_dir.mkdir(
        exist_ok=True
    )

    file_path = output_dir / filename

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "RESEARCH REPORT\n"
        )

        file.write(
            "===============\n\n"
        )

        file.write(
            f"TITLE\n"
        )

        file.write(
            f"{report.title}\n\n"
        )

        file.write(
            "EXECUTIVE SUMMARY\n"
        )

        file.write(
            "------------------\n"
        )

        file.write(
            f"{report.executive_summary}\n\n"
        )

        file.write(
            "KEY FINDINGS\n"
        )

        file.write(
            "------------\n"
        )

        for index, finding in enumerate(
            report.key_findings,
            start=1
        ):

            file.write(
                f"{index}. {finding}\n"
            )

        file.write("\n")

        file.write(
            "DETAILED ANALYSIS\n"
        )

        file.write(
            "-----------------\n"
        )

        file.write(
            f"{report.detailed_analysis}\n\n"
        )

        file.write(
            "FACT-CHECKED CLAIMS\n"
        )

        file.write(
            "--------------------\n"
        )

        for index, claim in enumerate(
            report.fact_checked_claims,
            start=1
        ):

            file.write(
                f"{index}. {claim}\n"
            )

        file.write("\n")

        file.write(
            "CONCLUSION\n"
        )

        file.write(
            "----------\n"
        )

        file.write(
            f"{report.conclusion}\n\n"
        )

        file.write(
            "SOURCES\n"
        )

        file.write(
            "-------\n"
        )

        for index, source in enumerate(
            report.sources,
            start=1
        ):

            file.write(
                f"{index}. {source}\n"
            )

    return file_path