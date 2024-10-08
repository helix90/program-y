import csv
import os
import os.path
from optparse import OptionParser


class CmdArgsHandler:

    def validate_args(self):
        parser = OptionParser()
        parser.add_option(
            "-f",
            "--file",
            dest="csvloc",
            help="Specify the location and filename of the CSV file.",
        )
        parser.add_option(
            "-d",
            "--directory",
            dest="dir",
            help="Specify the directory which contains the CSV.",
        )
        parser.add_option(
            "-o",
            "--output",
            dest="aimlloc",
            help="Specify the location where the aiml file should go.",
        )

        (opts, _) = parser.parse_args()

        mandatories = ["aimlloc"]
        self.check_manditory_opts_present(parser, opts, mandatories)
        return opts

    def check_manditory_opts_present(self, parser, opts, mandatories):

        for option in mandatories:
            if not opts.__dict__[option]:
                print("ERROR: Mandatory argument is missing.\n")
                parser.print_help()
                exit(-1)

        if not opts.csvloc and not opts.dir:
            print("ERROR: Enter the csv file location, or the directory.\n")
            parser.print_help()
            exit(-1)


class CsvReader:

    def __init__(self, file_name):
        self.file_name = file_name
        self.csvlength = 0

    def read_file(self):
        if not os.path.exists(self.file_name):
            print(self.file_name + " is not a valid file.")
            exit(-1)

        collection = []
        with open(self.file_name, "r") as f:
            reader = csv.reader(f)
            for linenum, row in enumerate(reader):
                if str(row).find("#") != -1:
                    continue
                if str(row).find(",") != -1:
                    collection.append([linenum + 1] + row)
                    self.csvlength += 1
        return collection


class CollectionLoader:

    def __init__(self, csv_file_name):
        self.csv_file_name = csv_file_name

    def get_collection(self):
        read = CsvReader(self.csv_file_name)
        collection = read.read_file()
        self.csvlength = read.csvlength
        return collection

    def format_collection(self, collection):
        parser = SentenceParser(collection[1:])  # omit line number
        return parser.populate()


class XmlWriter:

    def __init__(self, output_loc, file_name):
        self.aiml_file = open(output_loc + file_name + ".aiml", "w")

    def prepare_sentence(self, sentence):
        sentence.pop(0)
        value = " ".join(sentence)
        return value

    def write_body(self, sentence):
        template_content = sentence[0]
        pattern_text = self.prepare_sentence(sentence)
        self.aiml_file.write("\n\t<category>")
        self.aiml_file.write("\n\t\t<pattern>")
        self.aiml_file.write(pattern_text.upper())
        self.aiml_file.write("</pattern>")
        self.aiml_file.write("\n\t\t<template>")
        self.aiml_file.write(template_content)
        self.aiml_file.write("\n\t\t</template>")
        self.aiml_file.write("\n\t</category>")

    def open_file(self):
        self.aiml_file.write("<?xml version='1.0' encoding='ISO-8859-1'?>")
        self.aiml_file.write('\n<aiml version="1.0.1">')
        self.aiml_file.write(
            """\n
\t<!--  -->
\t<!-- This AIML file has been auto generated by the Program-Y util aiml_generator. -->
\t<!--  -->
\t<!-- Y-Bot is Copyright &copy; 2017 by Keith Sterling. -->
\t<!--
\tPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
\tdocumentation files (the "Software"), to deal in the Software without restriction, including without limitation
\tthe rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
\tand to permit persons to whom the Software is furnished to do so, subject to the following conditions:

\tThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

\tTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
\tTHE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
\tAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
\tTORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
\t-->
    """
        )

    def close_file(self):
        self.aiml_file.write("\n</aiml>\n")
        self.aiml_file.close()


class SentenceParser:

    def __init__(self, sentence):
        self.sentence = sentence

    def get_sentence_element(self, i):
        return self.sentence[i].strip()

    def get_sentence_length(self):
        return len(self.sentence)

    def parser(self, trees, branch, count):
        if self.get_sentence_length() <= count:
            return

        word = self.get_sentence_element(count)

        # Optional word
        if "(" in word and count > 0:
            alt = branch[:]
            alt.append(word.strip("()"))
            trees.append(alt)
            self.parser(trees, branch, count + 1)
            self.parser(trees, alt, count + 1)

        # One from the list
        elif word.count("|") > 0:

            split = word.split("|")
            options = len(split)

            for i in range(1, options):
                alt = branch[:]
                alt.append(split[i])
                trees.append(alt)
                self.parser(trees, alt, count + 1)

            branch.append(split[0])
            self.parser(trees, branch, count + 1)

        # Only one word allowed by csv column
        elif (count > 0) and (word.count(" ") > 0):
            print("WARNING: Comma missing in file [%s]" % word)
            branch.append(word)
            self.parser(trees, branch, count + 1)

        # Single word
        else:
            branch.append(word)
            self.parser(trees, branch, count + 1)

    def populate(self):
        trees = []
        branch = []
        trees.append(branch)
        self.parser(trees, branch, 0)
        return trees


class Generator:
    def __init__(self):
        self.categories = {}

    def get_aiml_file_name(self, csv_file_name):
        initial_split = csv_file_name.split("/")
        i = len(initial_split)
        secondary_split = initial_split[i - 1].split(".")

        return secondary_split[0]

    def generate_one(self, opts, csv_loc):
        cl = CollectionLoader(csv_loc)

        collections = cl.get_collection()
        if not collections:
            print(csv_loc + " has no content.")
            return
        aiml_file_name = self.get_aiml_file_name(csv_loc)

        xml = XmlWriter(opts.aimlloc, aiml_file_name)
        xml.open_file()

        for collection in collections:
            parsed_collection = cl.format_collection(collection)
            for rule in parsed_collection:
                xml.write_body(rule)

        xml.close_file()

    def get_files_in_dir(self, opts):
        if not os.path.exists(opts.dir):
            print(opts.dir + " is not a valid directory.")
            exit(-1)

        file_names = []
        for file in os.listdir(opts.dir):
            if file.endswith(".csv"):
                file_names.append(str(os.path.join(opts.dir, file)))
        if not file_names:
            print(
                "FATAL: There are no CSV files at this location.\n Are you in the right directory?"
            )
            exit(-1)

        return file_names


if __name__ == "__main__":

    cmd = CmdArgsHandler()
    opts = cmd.validate_args()
    g = Generator()

    if not opts.aimlloc.endswith("/"):
        opts.aimlloc = opts.aimlloc + "/"

    if not os.path.exists(opts.aimlloc):
        print(opts.aimlloc + " is not a valid output directory.")
        exit(-1)

    if opts.dir:
        if not opts.dir.endswith("/"):
            opts.dir = opts.dir + "/"

        file_names = g.get_files_in_dir(opts)
        for csv_file in file_names:
            g.generate_one(opts, csv_file)
    else:
        g.generate_one(opts, opts.csvloc)
