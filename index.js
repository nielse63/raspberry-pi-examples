require("dotenv").config();
const cp = require("child_process");
const path = require("path");
const chokidar = require("chokidar");

const exec = (cmd) => {
  return new Promise((resolve, reject) => {
    const [executable, ...args] = cmd.split(" ");
    const script = cp.spawn(executable, args);
    script.stdout.on("data", (data) => {
      console.log(data.toString());
    });

    script.on("close", (code) => {
      if (code) {
        return reject(code);
      }
      resolve();
    });
  });
};

let IS_RUNNING = false;
chokidar
  .watch(["**/*.py", "*.txt"], {
    ignored: [/(^|[\/\\])\../, "dist", "*.egg-info"],
  })
  .on("all", async (event, filepath) => {
    if (IS_RUNNING) return;
    IS_RUNNING = true;
    let abspath = path.join(__dirname, filepath);
    let remotePath = path.join(process.env.REMOTE_PATH, filepath);
    if (event === "unlink" || event === "unlinkDir") {
      abspath = path.dirname(abspath) + "/";
      remotePath = path.dirname(remotePath) + "/";
      // try {
      //   await exec("./copy-to-remote.sh");
      // } catch (error) {
      //   console.error(error);
      // }
      // return;
    }
    const cmd = `rsync -avzrptl --delete ${abspath} ${process.env.REMOTE_HOST}:${remotePath}`;
    try {
      await exec(cmd);
    } catch (error) {
      console.log({ error });
    }
    IS_RUNNING = false;
  });
