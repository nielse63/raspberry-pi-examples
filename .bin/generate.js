#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const readline = require("readline");
const { stdin: input, stdout: output } = require("process");
const snakeCase = require("lodash.snakecase");
const kebabCase = require("lodash.kebabcase");
const startCase = require("lodash.startcase");

const fsp = fs.promises;
const rl = readline.createInterface({ input, output });

// const kebabCase = (str) => {
//   return str.replace(/([a-z])([A-Z])/g, "$1-$2").toLowerCase();
// };

// const snakeCase = (str) => {
//   return str.replace(/([A-Z])/g, (g) => `-${g[0].toLowerCase()}`);
// };

const ensureDir = async (dir) => {
  try {
    await fsp.mkdir(dir);
  } catch (error) {
    if (error.code !== "EEXIST") {
      throw error;
    }
  }
};

const generateReadme = async ({ title, dir, snakeName, kebabName }) => {
  console.log("generating readme");
  const template = `# ${title}

- [Products](#products)
- [Wiring](#wiring)
- [Setup](#setup)
- [Usage](#usage)

## Products

- ...

## Wiring

| DS18B20 | Raspberry Pi |
| ------- | ------------ |
| VCC     | 3v3          |
| GND     | GND          |
| ...     | ...          |

![${title}](../assets/${path.basename(dir)}.jpg)

## Setup

Install dependencies:

\`\`\`bash
sudo apt-get update -y
sudo apt-get updgrade -y
sudo apt-get install build-essential python-dev -y
python3 -m pip install pkg1 pkg2
\`\`\`

## Usage

\`\`\`bash
python3 ./${snakeName}.py
\`\`\`
`;
  await fsp.writeFile(path.resolve(dir, "README.md"), template);
};

const generateScript = async ({ name, title, dir, snakeName }) => {
  console.log("generating python file");
  const template = `#!/usr/bin/env python3
import time

def main():
    print("Running ${title}")

if __name__ == "__main__":
    main()
`;
  await fsp.writeFile(path.resolve(dir, `${snakeName}.py`), template);
};

const question = (message) => {
  return new Promise((resolve) => {
    rl.question(message, (answer) => {
      resolve(answer);
    });
  });
};

const main = async () => {
  const name = await question("Name: ");
  const type = await question("Type: ");
  const title = startCase(`${name} ${type}`);
  rl.close();

  const snakeName = snakeCase(name);
  const kebabName = kebabCase(name);
  const dir = path.resolve(__dirname, "../", `${kebabName}-${type}`);
  const data = { name, title, type, dir, snakeName, kebabName };
  await ensureDir(dir);
  await generateReadme(data);
  await generateScript(data);
  console.log("done");
};

main().catch(console.error);
