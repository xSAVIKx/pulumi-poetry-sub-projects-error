import pulumi
from pulumi_gcp import cloudfunctions, storage

source_bucket = storage.Bucket(
    resource_name="some-source-bucket-for-tests-only",
    force_destroy=True
)
source_archive: storage.BucketObject = storage.BucketObject(
    resource_name=f"gcf-sources",
    bucket=source_bucket.name,
    content_type="application/zip",
    source=pulumi.asset.AssetArchive(
        {
            "requirements.txt": pulumi.asset.FileAsset(f"./deployable/requirements.txt"),
            "main.py": pulumi.asset.FileAsset(f"./deployable/main.py"),
            "deployable/": pulumi.asset.FileArchive(f"./deployable/deployable/"),
            "dist/deps": pulumi.asset.FileArchive(f"./deployable/dist/deps"),
        }
    ),
    opts=pulumi.ResourceOptions(parent=source_bucket),
)
cloudfunctions.Function(
    resource_name=f"test-gcf",
    source_archive_bucket=source_bucket.name,
    source_archive_object=source_archive.name,
    entry_point="handle",
    runtime="python38",
    trigger_http=True,
)
