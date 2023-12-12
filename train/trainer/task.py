import argparse
from trainer import train_model


def get_args():
    """Define the task arguments with the default values.

    Returns:
        experiment parameters
    """
    args_parser = argparse.ArgumentParser()
    
    # Saved model arguments
    args_parser.add_argument(
        '--model-name',
        default="default-zephyr7b-gptq",
        help='The name of your saved model')

    return args_parser.parse_args()


def main():
    """Setup / Start the experiment
    """
    args = get_args()
    print(args)
    train_model.run(args)


if __name__ == '__main__':
    main()